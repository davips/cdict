from hoshmap.value.ival import iVal


class CacheableiVal(iVal):
    replace: callable
    deps:dict

    def __init__(self, caches=None):
        self.caches = caches

    def withcaches(self, caches):
        if self.caches is not None:
            self.caches.append(caches)
        return self.replace(caches=caches)

    def __repr__(self):
        if not self.isevaluated:
            return f"←({' '.join(k + ('' if dep.isevaluated else repr(dep)) for k, dep in self.deps.items())})"
        return repr(self.value)
