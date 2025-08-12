from pytest import File, Item

class YamlFile(File):
    def collect(self):
        # We need a yaml parser, e.g. PyYAML.
        import yaml

        raw = yaml.safe_load(self.path.open(encoding="utf-8"))
        yield YamlTags.from_parent(self, name=f"Pipeline Tags", yaml=raw)
        yield PipelineNamingConvention.from_parent(self, name=f"Pipeline Name", yaml=raw)

class YamlItem(Item):
    def __init__(self, *, yaml, **kwargs):
        super().__init__(**kwargs)
        self.yaml = yaml

    def repr_failure(self, excinfo):
        """Called when self.runtest() raises an exception."""
        if isinstance(excinfo.value, YamlException):
            return "\n".join(excinfo.value.args)
        return super().repr_failure(excinfo)

    def reportinfo(self):
        return self.path, 0, f"{self.name}: {str(self.path).replace(f"{str(self.config.rootdir)}/", '')}"


class YamlTags(YamlItem):
    def runtest(self):
        if 'streamtags' not in self.yaml or len(self.yaml['streamtags']) == 0:
            raise YamlException("* No tags found *", "All pipelines must have at least one tag")

class PipelineNamingConvention(YamlItem):
    def runtest(self):
        pipeline_name = str(self.path).split('/')[-2]
        if not pipeline_name.startswith("pipeline_"):
            raise YamlException("* Invalid pipeline name *", f"Pipeline name '{pipeline_name}' does not follow the naming convention 'pipeline_*'")

class YamlException(Exception):
    """Custom exception for error reporting."""
