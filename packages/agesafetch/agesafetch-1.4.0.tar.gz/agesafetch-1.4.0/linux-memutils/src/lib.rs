// SPDX-FileCopyrightText: Benedikt Vollmerhaus <benedikt@vollmerhaus.org>
// SPDX-License-Identifier: MIT
/*!
This crate provides basic utilities for reading from physical memory on Linux.

It is developed in tandem with the `agesafetch` binary crate, but some of its
features may come in handy for other use cases.
*/
pub mod agesa;
pub mod iomem;
pub mod reader;
