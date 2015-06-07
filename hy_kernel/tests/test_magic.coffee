casper.notebook_test ->

  cells = {}

  capture = require("./capture") @, "magic"

  @then ->
    @viewport 1024, 768, ->
      @evaluate -> IPython.kernelselector.set_kernel "hy"
      @wait_for_idle()

  # cell magic that compiles
  @then ->
    @execute_cell cells.hymagic = @append_cell """
      %%timeit
      (+ 1 1)
      """, "code"

  @wait_for_idle()

  capture "cell-magic-er"

  @then ->
    @test.assertMatch @get_output_cell(cells.hymagic, 0).text,
      /loops/,
      "a cell magic that compiles hy works"


  # cell magic that doesn't compile
  @then ->
    @execute_cell cells.plaincell = @append_cell """
      %%%HTML
      <h1>Magic!</h1>
      """, "code"

  @wait_for_idle()

  capture "cell-plain"

  @then ->
    @test.assertSelectorHasText "h1", "Magic!",
      "a cell magic that doesn't compile hy works"


  # ! line magic
  @then ->
    @execute_cell cells.bangline = @append_cell """
      !ls
      """, "code"

  capture "line-bang"

  @then ->
    @test.assertMatch @get_output_cell(cells.bangline, 0).text,
      /Untitled/,
      "bang line magic works"


  # % line magic
  @then ->
    @execute_cell cells.percline = @append_cell """
      %ls
      """, "code"

  @wait_for_idle()

  capture "line-perc"

  @then ->
    @test.assertMatch @get_output_cell(cells.percline, 0).text,
      /Untitled/,
      "percent line magic works"
