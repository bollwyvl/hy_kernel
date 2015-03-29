# val = the value to pad
# length = the length of the padded string
# padChar = the character to use for padding.  Defaults to '0'
pad = (val, length, padChar = '0') ->
  val += ''
  numPads = length - val.length
  if (numPads > 0) then new Array(numPads + 1).join(padChar) + val else val

module.exports = (casper, prefix="") ->
  _cid = 0
  capture = (name) ->
    casper.then ->
      @capture ["screenshots", prefix, "#{pad _cid++, 3}_#{name}.png"].join "/"
