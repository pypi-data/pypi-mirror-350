/*
 * Copyright (C) 2023 Dominik Drexler and Simon Stahlberg
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program. If not, see <https://www.gnu.org/licenses/>.
 */

#ifndef MIMIR_SEARCH_HEURISTICS_INTERFACE_HPP_
#define MIMIR_SEARCH_HEURISTICS_INTERFACE_HPP_

#include "mimir/search/declarations.hpp"

namespace mimir::search
{

/**
 * Interface class
 */

class IHeuristic
{
public:
    virtual ~IHeuristic() = default;

    virtual ContinuousCost compute_heuristic(State state, bool is_goal_state) = 0;
};

}

#endif