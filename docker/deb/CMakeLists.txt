# docker 

configure_file(prepare/Dockerfile prepare/Dockerfile)
configure_file(prepare/run.in prepare/run)

configure_file(build/Dockerfile.in build/Dockerfile)
configure_file(build/run.in build/run)

configure_file(test/Dockerfile.in test/Dockerfile)
configure_file(test/run.in test/run)

add_custom_target( 
  build-deb-deps
  COMMAND bash run
  WORKING_DIRECTORY prepare
  )

# output under ..../build/DEB
add_custom_target( 
  build-deb
  COMMAND bash run
  WORKING_DIRECTORY build
  )
add_dependencies(build-deb build-deb-deps)

add_custom_target( 
  test-deb
  COMMAND bash run
  WORKING_DIRECTORY test
  )
