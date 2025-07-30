class DictUtil:
  @staticmethod
  def get(key:str, source:dict, fallback:any = None) -> any:
    return source[key] if source[key] is not None else fallback

  @staticmethod
  def clean(source:dict) -> dict:
    ret = {}
    for k, v in source.items():
      if v is not None:
        ret[k] = v
    return ret