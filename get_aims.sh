#!/bin/bash

awk '/AIMs will be reciprocally fixed \(0-based index\):/,/These observed differences will be treated as polymorphic \(0-based index\):/' hybrid_genomes_log > AIMS_out

tail -n +2 AIMS_out | head -n -1 | sort -n > AIMS_sort
