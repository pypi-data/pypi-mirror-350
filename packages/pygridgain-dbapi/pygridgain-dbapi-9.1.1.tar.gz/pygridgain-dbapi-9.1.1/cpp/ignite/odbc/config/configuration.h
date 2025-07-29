/*
 *  Copyright (C) GridGain Systems. All Rights Reserved.
 *  _________        _____ __________________        _____
 *  __  ____/___________(_)______  /__  ____/______ ____(_)_______
 *  _  / __  __  ___/__  / _  __  / _  / __  _  __ `/__  / __  __ \
 *  / /_/ /  _  /    _  /  / /_/ /  / /_/ /  / /_/ / _  /  _  / / /
 *  \____/   /_/     /_/   \_,__/   \____/   \__,_/  /_/   /_/ /_/
 */

#pragma once

#include "ignite/odbc/config/config_tools.h"
#include "ignite/odbc/config/value_with_default.h"

#include "ignite/common/end_point.h"

#include <cstdint>
#include <string>

namespace ignite {

/**
 * ODBC configuration abstraction.
 */
class configuration {
public:
    /** Default values for configuration. */
    struct default_value {
        /** Default value for fetch results page size attribute. */
        static inline const std::int32_t page_size{1024};

        /** Default value for Driver attribute. */
        static inline const std::string host{"localhost"};

        /** Default value for TCP port attribute. */
        static inline const std::uint16_t port{10800};

        /** Default value for Address attribute. */
        static inline const std::vector<end_point> address{{host, port}};

        /** Default value for Schema attribute. */
        static inline const std::string schema{"PUBLIC"};

        /** Default value for Timezone attribute. */
        static inline const std::string timezone{};
    };

    // Default.
    configuration() = default;

    // With auth.
    configuration(std::string identity, std::string secret)
        : m_auth_identity{std::move(identity), true}
        , m_auth_secret{std::move(secret), true} {}

    /**
     * Get addresses.
     *
     * @return Addresses.
     */
    [[nodiscard]] const value_with_default<std::vector<end_point>> &get_address() const { return m_end_points; }

    /**
     * Set addresses.
     *
     * @param addr Addresses.
     */
    void set_address(std::string addr) { m_end_points = {parse_address(addr), true}; }

    /**
     * Get fetch results page size.
     *
     * @return Fetch results page size.
     */
    [[nodiscard]] const value_with_default<std::int32_t> &get_page_size() const { return m_page_size; }

    /**
     * Set fetch results page size.
     *
     * @param page_size Fetch results page size.
     */
    void set_page_size(std::int32_t page_size) { m_page_size = {page_size, true}; }

    /**
     * Get schema.
     *
     * @return Schema.
     */
    [[nodiscard]] const value_with_default<std::string> &get_schema() const { return m_schema; }

    /**
     * Set schema.
     *
     * @param schema Schema.
     */
    void set_schema(std::string schema) { m_schema = {std::move(schema), true}; }

    /**
     * Get authentication type.
     *
     * @return Authentication type.
     */
    [[nodiscard]] const std::string &get_auth_type() const { return TYPE; };

    /**
     * Get identity.
     *
     * @return Identity.
     */
    [[nodiscard]] const value_with_default<std::string> &get_auth_identity() const { return m_auth_identity; };

    /**
     * Set identity.
     *
     * @param identity Identity.
     */
    void set_auth_identity(std::string identity) { m_auth_identity = {std::move(identity), true}; }

    /**
     * Get secret.
     *
     * @return Secret.
     */
    [[nodiscard]] const value_with_default<std::string> &get_auth_secret() const { return m_auth_secret; };

    /**
     * Set secret.
     *
     * @param secret Secret.
     */
    void set_auth_secret(std::string secret) { m_auth_secret = {std::move(secret), true}; }

    /**
     * Get Timezone.
     *
     * @return Timezone.
     */
    [[nodiscard]] const value_with_default<std::string> &get_timezone() const { return m_timezone; };

    /**
     * Fill from configuration params.
     *
     * @throw odbc_error On parsing error.
     * @param config_params Configuration params
     */
    void from_config_map(const config_map &config_params);

private:
    /** Type constant. */
    inline static const std::string TYPE{"basic"};

    /** Request and response page size. */
    value_with_default<std::int32_t> m_page_size{default_value::page_size, false};

    /** Connection end-points. */
    value_with_default<std::vector<end_point>> m_end_points{default_value::address, false};

    /** Schema. */
    value_with_default<std::string> m_schema{default_value::schema, false};

    /** Identity. */
    value_with_default<std::string> m_auth_identity{"", false};

    /** Secret. */
    value_with_default<std::string> m_auth_secret{"", false};

    /** Timezone. */
    value_with_default<std::string> m_timezone{"", false};
};

} // namespace ignite
