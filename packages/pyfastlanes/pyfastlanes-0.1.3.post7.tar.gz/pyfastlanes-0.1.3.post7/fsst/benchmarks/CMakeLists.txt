add_executable(test_fsst test_fsst.cpp)
target_link_libraries(test_fsst PUBLIC gtest_main gmock_main FastLanes)
gtest_discover_tests(test_fsst)

add_executable(test_fls_fsst test_fls_fsst.cpp)
target_link_libraries(test_fls_fsst PUBLIC gtest_main gmock_main FastLanes)
gtest_discover_tests(test_fls_fsst)
