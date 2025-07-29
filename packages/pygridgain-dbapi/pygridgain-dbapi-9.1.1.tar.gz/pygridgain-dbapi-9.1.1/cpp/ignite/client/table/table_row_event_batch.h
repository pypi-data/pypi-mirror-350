/*
 *  Copyright (C) GridGain Systems. All Rights Reserved.
 *  _________        _____ __________________        _____
 *  __  ____/___________(_)______  /__  ____/______ ____(_)_______
 *  _  / __  __  ___/__  / _  __  / _  / __  _  __ `/__  / __  __ \
 *  / /_/ /  _  /    _  /  / /_/ /  / /_/ /  / /_/ / _  /  _  / / /
 *  \____/   /_/     /_/   \_,__/   \____/   \__,_/  /_/   /_/ /_/
 */

#pragma once

#include "ignite/client/table/table_row_event.h"

#include <vector>

namespace ignite {

/**
 * Table row event batch.
 *
 * @tparam T Table row type.
 */
template<typename T>
class table_row_event_batch {
public:
    /** Value type. */
    typedef T value_type;

    // Default
    table_row_event_batch() = default;

    /**
     * Constructor.
     *
     * @param events Events.
     */
    explicit table_row_event_batch(std::vector<table_row_event<value_type>> &&events)
        : m_events(std::move(events)) {}

    /**
     * Gets the events.
     *
     * @return Events.
     */
    [[nodiscard]] const std::vector<table_row_event<value_type>> &get_events() const & { return m_events; }

    /**
     * Gets the events.
     *
     * @return Events.
     */
    [[nodiscard]] std::vector<table_row_event<value_type>> &&get_events() && { return std::move(m_events); }

private:
    /** Table row events. */
    std::vector<table_row_event<value_type>> m_events;
};

} // namespace ignite
