from django.core.files.images import ImageFile
from django.db.models.fields.files import FieldFile, ImageField


class SysconImageFieldFile(ImageFile, FieldFile):
    @property
    def src_path(self):
        if self:
            if str(self).startswith("http"):
                return str(self)
            else:
                return self.url

        return ""


class SysconImageField(ImageField):
    attr_class = SysconImageFieldFile
