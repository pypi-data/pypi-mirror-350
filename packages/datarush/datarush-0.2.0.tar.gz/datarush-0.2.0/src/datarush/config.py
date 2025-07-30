"""Application config."""

from enum import StrEnum

from dotenv import load_dotenv
from envarify import AnyHttpUrl, BaseConfig, EnvVar, SecretString

load_dotenv()


################################
########## S3 CONFIG ###########
################################


class S3Config(BaseConfig):
    """S3 Configuration."""

    endpoint: AnyHttpUrl = EnvVar("S3_ENDPOINT")
    access_key: str = EnvVar("S3_ACCESS_KEY")
    secret_key: SecretString = EnvVar("S3_SECRET_KEY")
    default_bucket: str | None = EnvVar("S3_DEFAULT_BUCKET", default=None)


################################
#### TEMPLATE STORE CONFIG #####
################################


class TemplateStoreType(StrEnum):
    """Template Store Type."""

    S3 = "S3"
    FILESYSTEM = "FILESYSTEM"


class S3TemplateStoreConfig(BaseConfig):
    """S3 based template manager config."""

    bucket: str = EnvVar("TEMPLATE_STORE_S3_BUCKET")
    prefix: str = EnvVar("TEMPLATE_STORE_S3_PREFIX", default="datarush")


class FilesystemTemplateStoreConfig(BaseConfig):
    """File system based template manager config."""

    path: str = EnvVar("TEMPLATE_STORE_FILESYSTEM_PATH", default=".")


class TemplateStoreConfig(BaseConfig):
    """Template Manager Configuration."""

    store_type: TemplateStoreType = EnvVar("TEMPLATE_STORE_TYPE")

    @property
    def s3(self) -> S3TemplateStoreConfig:
        """S3 template store config."""
        if self.store_type != TemplateStoreType.S3:
            raise ValueError("Template store type is not S3")
        return S3TemplateStoreConfig.fromenv()

    @property
    def filesystem(self) -> FilesystemTemplateStoreConfig:
        """File system template store config."""
        if self.store_type != TemplateStoreType.FILESYSTEM:
            raise ValueError("Template store type is not FILESYSTEM")
        return FilesystemTemplateStoreConfig.fromenv()


################################
###### APPLICATION CONFIG ######
################################


class AppConfig(BaseConfig):
    """Application Configuration."""

    s3: S3Config
    template_store: TemplateStoreConfig
