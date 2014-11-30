casper.notebook_test ->
  cells = {}

  @then ->
    @viewport 1024, 768
    @click "#current_kernel_spec"
    
  @then ->
    @test.assertExists "#kernel-hy a", "is available"
  
  @then ->
    @click "#kernel-hy a"


  @wait 5000
  @wait_for_idle()
    
  @then ->
    @execute_cell cells.addition = @append_cell "(+ 1 1)", "code"
  @wait_for_idle()
  
  @then -> @capture "screenshots/1_plus_1.png"

  @then ->
    @test.assertMatch @get_output_cell(cells.addition, 0).data["text/plain"],
      /^2L?$/,
      "adding 1 to 1 gives 2"

  @then ->
    @execute_cell cells.setx = @append_cell "(setv x 1)", "code"
  @then ->
    @execute_cell cells.printx = @append_cell "x", "code"

  @wait_for_idle()

  @then -> @capture "screenshots/setv_x_1.png"

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

  @then -> @capture "screenshots/magic.png"

  @then ->
    @test.assertMatch @get_output_cell(cells.magic, 0).text,
      /loops/,
      "a cell magic works"

    