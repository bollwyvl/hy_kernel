casper.test.begin "use the Hy kernel", ->
  casper.notebook_test ->
    cells = {}

    @then ->
      @viewport 1024, 768
      @click "#current_kernel_spec"
    
    @then ->
      @test.assertExists "#kernel-hy a", "the kernel is available"

    @then ->
      @click "#kernel-hy a"
      
    @wait_for_idle()
    
    @then ->
      @execute_cell cells.addition = @append_cell "(+ 1 1)", "code"
    @then ->
      @test.assertEquals "2", @get_output_cell(cells.addition, 0)["text/plain"],
        "adding 1 to 1 gives 2"

    @then ->
      @execute_cell cells.setx = @append_cell "(setv x 1)", "code"
    @then ->
      @execute_cell cells.printx = @append_cell "x", "code"
    @wait_for_idle()
    @then ->
      @test.assertEquals "1",
        @get_output_cell(cells.printx , 0)["text/plain"],
        "variables persist"
        
    @then ->
      @execute_cell cells.magic = @append_cell """
      %%timeit
      (+ 1 1)
      """, "code"
    @wait_for_idle()
    @then ->
      @log @get_output_cell(cells.magic, 0)
      @test.assertMatch @get_output_cell(cells.magic, 0).text,
        /loops/,
        "a cell magic works"

    @then ->
      @capture "foo.png"
    