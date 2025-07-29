/*
 *  Copyright (C) GridGain Systems. All Rights Reserved.
 *  _________        _____ __________________        _____
 *  __  ____/___________(_)______  /__  ____/______ ____(_)_______
 *  _  / __  __  ___/__  / _  __  / _  / __  _  __ `/__  / __  __ \
 *  / /_/ /  _  /    _  /  / /_/ /  / /_/ /  / /_/ / _  /  _  / / /
 *  \____/   /_/     /_/   \_,__/   \____/   \__,_/  /_/   /_/ /_/
 */

#pragma once

#include "ignite/client/transaction/transaction.h"

#include "ignite/common/detail/config.h"
#include "ignite/common/ignite_result.h"

#include <memory>

namespace ignite {

namespace detail {
class transactions_impl;
}

/**
 * Ignite transactions.
 */
class transactions {
    friend class ignite_client;

public:
    // Delete
    transactions() = delete;

    /**
     * Starts a new transaction.
     *
     * @return A new transaction.
     */
    IGNITE_API transaction begin() {
        return sync<transaction>([this](auto callback) { begin_async(std::move(callback)); });
    }

    /**
     * Starts a new transaction asynchronously.
     *
     * @param callback Callback to be called with a new transaction or error upon completion of asynchronous operation.
     */
    IGNITE_API void begin_async(ignite_callback<transaction> callback);

private:
    /**
     * Constructor
     *
     * @param impl Implementation
     */
    explicit transactions(std::shared_ptr<detail::transactions_impl> impl)
        : m_impl(std::move(impl)) {}

    /** Implementation. */
    std::shared_ptr<detail::transactions_impl> m_impl;
};

} // namespace ignite
