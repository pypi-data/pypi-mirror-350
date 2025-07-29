/*
 *  Copyright (C) GridGain Systems. All Rights Reserved.
 *  _________        _____ __________________        _____
 *  __  ____/___________(_)______  /__  ____/______ ____(_)_______
 *  _  / __  __  ___/__  / _  __  / _  / __  _  __ `/__  / __  __ \
 *  / /_/ /  _  /    _  /  / /_/ /  / /_/ /  / /_/ / _  /  _  / / /
 *  \____/   /_/     /_/   \_,__/   \____/   \__,_/  /_/   /_/ /_/
 */

#include "ignite_runner_suite.h"

#include <ignite/client/basic_authenticator.h>
#include <ignite/client/ignite_client.h>
#include <ignite/client/ignite_client_configuration.h>

#include <gtest/gtest.h>

#include <chrono>

using namespace ignite;

/**
 * Test suite.
 */
class client_test : public ignite_runner_suite {};

TEST_F(client_test, get_configuration) {
    ignite_client_configuration cfg{get_node_addrs()};
    cfg.set_logger(get_logger());
    cfg.set_connection_limit(42);

    auto client = ignite_client::start(cfg, std::chrono::seconds(30));

    const auto &cfg2 = client.configuration();

    EXPECT_EQ(cfg.get_endpoints(), cfg2.get_endpoints());
    EXPECT_EQ(cfg.get_connection_limit(), cfg2.get_connection_limit());
}