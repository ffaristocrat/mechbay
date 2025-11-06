libc = {
  getvalue = function(f)
    return assert(load(string.format("return %s", f)))()
  end,
  setvalue = function(f, v)
    if type(v) == "string" then
      assert(load(string.format("%s=\"%s\"", f, v)))()
    else
      assert(load(string.format("%s=%s", f, v)))()
    end
  end,
  getsize = function(f)
    return assert(load(string.format("return rawlen(%s)", f)))()
  end
}
