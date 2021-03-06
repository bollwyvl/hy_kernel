casper.notebook_test ->
  cells = {}

  capture = require("./capture") @, "complete"

  @then ->
    @viewport 1024, 768, ->
      @evaluate -> IPython.kernelselector.set_kernel "hy"
      @wait_for_idle()

  @thenEvaluate ->
    IPython.notebook.insert_cell_at_index 0, "code"
    cell = IPython.notebook.get_cell 0
    cell.set_text "(unquote"
    cell.focus_editor()
  @then ->
    @page.sendEvent 'keypress', @page.event.key.End
    @page.sendEvent 'keypress', @page.event.key.Tab
  @wait 100
  @then ->
    @test.assertExists "#complete .introspection", "hy completions available"

  capture "complete"
