casper.notebook_test ->

  cells = {}

  capture = require("./capture") @, "basic"

  @then ->
    @viewport 1024, 768, ->
      @evaluate -> IPython.kernelselector.set_kernel "hy"
      @wait_for_idle()

  capture "hy_kernel"

  @then -> @execute_cell cells.addition = @append_cell "(+ 1 1)", "code"
  @wait_for_idle()

  capture "1_plus_1"

  @then ->
    @test.assertMatch @get_output_cell(cells.addition, 0).data["text/plain"],
      /^2L?$/,
      "adding 1 to 1 gives 2"

  @then ->
    @execute_cell cells.setx = @append_cell "(setv x 1)", "code"
  @then ->
    @execute_cell cells.printx = @append_cell "x", "code"

  @wait_for_idle()

  capture "setv_x_1"

  @then ->
    @test.assertMatch @get_output_cell(cells.printx , 0).data["text/plain"],
      /^1L?$/,
      "variables persist"

  @then ->
    @execute_cell cells.magic = @append_cell """
    %%timeit
    (+ 1 1)
    """, "code"

  @wait_for_idle()

  capture "magic"

  @then ->
    @test.assertMatch @get_output_cell(cells.magic, 0).text,
      /loops/,
      "a cell magic works"

  @wait_for_idle()

  @then ->
    @execute_cell cells.usefor = @append_cell "(for [i (range 3)] (print i))", "code"

  @wait_for_idle()

  capture "use_for"

  @then ->
    @test.assertMatch @get_output_cell(cells.usefor, 0).text,
      /^0\n1\n2\n$/,
      "using `for` works"
