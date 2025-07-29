/*
 *  Copyright (C) GridGain Systems. All Rights Reserved.
 *  _________        _____ __________________        _____
 *  __  ____/___________(_)______  /__  ____/______ ____(_)_______
 *  _  / __  __  ___/__  / _  __  / _  / __  _  __ `/__  / __  __ \
 *  / /_/ /  _  /    _  /  / /_/ /  / /_/ /  / /_/ / _  /  _  / / /
 *  \____/   /_/     /_/   \_,__/   \____/   \__,_/  /_/   /_/ /_/
 */

#pragma once

#ifdef _WIN32
# include <windows.h>
#endif

#include "ignite_runner.h"
#include "odbc_connection.h"
#include "odbc_test_utils.h"
#include "test_utils.h"

#include "tests/test-common/basic_auth_test_suite.h"

#include <gtest/gtest.h>

#include <memory>
#include <string_view>

#include <sql.h>
#include <sqlext.h>

namespace ignite {

/**
 * Test suite.
 */
class odbc_suite : public virtual ::testing::Test, public odbc_connection {
public:
    // TODO https://issues.apache.org/jira/browse/IGNITE-24261 revert changing named to uppercase
    static inline const std::string TABLE_1 = "TBL1";
    static inline const std::string TABLE_NAME_ALL_COLUMNS = "TBL_ALL_COLUMNS";
    static inline const std::string TABLE_NAME_ALL_COLUMNS_SQL = "TBL_ALL_COLUMNS_SQL";

    static constexpr const char *KEY_COLUMN = "key";
    static constexpr const char *VAL_COLUMN = "val";

    static inline const std::string DRIVER_NAME = "Apache Ignite 3";

    /**
     * Get node addresses to use for tests.
     *
     * @return Addresses.
     */
    static std::string get_nodes_address() {
        std::string res;
        for (const auto &addr : ignite_runner::get_node_addrs())
            res += addr + ',';

        return res;
    }

    /**
     * Get node addresses to use for tests.
     *
     * @return Addresses.
     */
    static std::string get_basic_connection_string() {
        return "driver={" + DRIVER_NAME + "};address=" + get_nodes_address() + ';';
    }
};

} // namespace ignite
