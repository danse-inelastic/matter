# docker 

configure_file(prepare/Dockerfile prepare/Dockerfile)
configure_file(prepare/run.in prepare/run)

configure_file(build/Dockerfile.in build/Dockerfile)
configure_file(build/run.in build/run)

configure_file(test/Dockerfile.in test/Dockerfile)
configure_file(test/run.in test/run)

add_custom_target( 
  build-srpm-deps
  COMMAND bash run
  WORKING_DIRECTORY prepare
  )

# output under ..../build/SRPMS/
add_custom_target( 
  build-srpm
  COMMAND bash run
  WORKING_DIRECTORY build
  )
add_dependencies(build-srpm build-srpm-deps)

add_custom_target( 
  test-srpm
  COMMAND bash run
  WORKING_DIRECTORY test
  )
