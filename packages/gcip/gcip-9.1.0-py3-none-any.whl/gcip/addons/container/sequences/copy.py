from dataclasses import dataclass
from typing import Union

from gcip.addons.container.jobs import crane, trivy
from gcip.addons.container.registries import Registry
from gcip.core.cache import Cache, CacheKey
from gcip.core.sequence import Sequence
from gcip.core.variables import PredefinedVariables


@dataclass(kw_only=True)
class CopyContainerOpts:
    image_name: str
    image_tag: str
    src_registry: Union[Registry, str] = Registry.DOCKER
    dst_registry: Union[Registry, str] = Registry.DOCKER
    do_trivy_scan: bool = True
    do_trivy_ignore_file_check: bool = True


class CopyContainer(Sequence):
    def __init__(
        self,
        *,
        image_name: str,
        image_tag: str,
        src_registry: Union[Registry, str] = Registry.DOCKER,
        dst_registry: Union[Registry, str] = Registry.DOCKER,
        do_trivy_scan: bool = True,
        do_trivy_ignore_file_check: bool = True,
        do_crane_direct_copy: bool = False,
    ) -> None:
        """
        Creates a `gcip.Sequence` to pull, scan and push a container image.

        The pull step is executed by `gcip.addons.container.jobs.crane.pull`, it will pull the container image an outputs it to a tarball.
        There is one addtional vulnerability scan with `gcip.addons.container.jobs.trivy.scan`. The output is uploaded as an artifact to the GitLab instance.
        Built container image is uploaded with `gcip.addons.container.jobs.crane.push`.

        Args:
            src_registry (Union[Registry, str], optional): Container registry to pull the image from. If the container registry needs authentication,
                you have to provide a `gcip.addons.container.config.DockerClientConfig` object with credentials. Defaults to Registry.DOCKER.
            dst_registry (Union[Registry, str]): Container registry to push the image to. If the container registry needs authentication,
                you have to provide a `gcip.addons.container.config.DockerClientConfig` object with credentials. Defaults to Registry.DOCKER.
            image_name (str): Image name with stage in the registry. e.g. username/image_name.
            image_tag (str): Container image tag to pull from `src_registry` and push to `dst_registry`.
            do_trivy_scan (Optional[bool]): Set to `False` to skip the Trivy scan job. Defaults to True.
            do_trivyignore_check (Optional[bool]): Set to `False` to skip the existance check of the `.trivyignore` file. Defaults to True.
            do_crane_direct_copy (Optional[bool]): If `True`, crane copies the image directly from the source to the destination without using
                the chache. If `False` (default), crane pushes the cached image from the crane-pull-job. This can alter the images digest.

        Returns:
            Sequence: `gcip.Sequence` to pull, scan and push a container image.
        """
        super().__init__()

        """
        We decided to use caches instead of artifacts to pass the Docker image tar archive from one job to another.
        This is because those tar archives could become very large - especially larger then the maximum artifact size limit.
        This limit can just be adjusted by the admin of the gitlab instance, so your pipeline would never work, your Gitlab
        provider would not adjust this limit for you. For caches on the other hand you can define storage backends at the
        base of your Gitlab runners.

        Furthermore we set the cache key to the pipeline ID. This is because the name and tag of the image does not ensure that
        the downloaded tar is unique, as the image behind the image tag could be overridden. So we ensure uniqueness by downloading
        the image once per pipeline.
        """

        self.cache = Cache(
            paths=["image"],
            cache_key=CacheKey(
                PredefinedVariables.CI_PIPELINE_ID + image_name + image_tag
            ),
        )

        #
        # crane pull
        #
        self.crane_pull_job = crane.Pull(
            src_registry=src_registry,
            image_name=image_name,
            image_tag=image_tag,
            tar_path=self.cache.paths[0],
        )
        self.crane_pull_job.set_cache(self.cache)
        if do_trivy_scan or not do_crane_direct_copy:
            self.add_children(self.crane_pull_job)

        #
        # trivy scan
        #
        self.trivy_scan_job = trivy.ScanLocalImage(
            image_name=image_name, image_path=self.cache.paths[0]
        )
        self.trivy_scan_job.set_cache(self.cache)
        self.trivy_scan_job.add_needs(self.crane_pull_job)
        if do_trivy_scan:
            self.add_children(self.trivy_scan_job)

        #
        # trivy ignore file check
        #
        self.trivy_ignore_file_check_job = trivy.TrivyIgnoreFileCheck()
        if do_trivy_ignore_file_check:
            self.add_children(self.trivy_ignore_file_check_job)

        #
        # crane push
        #
        self.crane_push_job: crane.Copy | crane.Push
        if do_crane_direct_copy:
            self.crane_push_job = crane.Copy(
                src_registry=src_registry,
                src_repository=image_name,
                src_tag=image_tag,
                dst_registry=dst_registry,
            )
        else:
            self.crane_push_job = crane.Push(
                dst_registry=dst_registry,
                image_name=image_name,
                image_tag=image_tag,
                tar_path=self.cache.paths[0],
            )
            self.crane_push_job.set_cache(self.cache)
            self.crane_push_job.add_needs(self.crane_pull_job)

        self.add_children(self.crane_push_job)

        if do_trivy_scan:
            self.crane_push_job.add_needs(self.trivy_scan_job)
