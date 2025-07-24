# Dev Flow

# The role and the task sets the scene

**Prompt:**

You are the PM of this project and is tasked for refactoring the flow and agents within it to a more sustainable and reduce the technical debt. The first step would be to generate appropriate unit tests, and then plan for how to split flow.py into smaller parts. Write a overarching sprint plan of 5 days to sprint_1.md.

**Example Output:**
- Overarching plan for sprint 1 in sprint_1.md.

# Writing specs

**Prompt:**
As a senior software developer, break down the sprint_1.md day 1 into specs, write each spec into specs subdirectory. Update sprint_1.md with the name of the spec file, a very brief summary of reason, and a status of development.

**Example Output:**
- specs/day1_spec1_testing_framework.md
- specs/day1_spec2_utility_testing.md
- specs/day1_spec3_history

# Implementing specs

**Prompt:**
As a senior python developer and qa engineer, implement the #specs/day1_spec1_testing_framework.md and update the spec and sprint_1.md with results to keep track of the progress. Do not stop until we have a working test suite.

**Example Output:**
- Lots of changes and tests run

# Next day


**Prompt:**
Day 2 of 5 in this @sprint_1.md. As a PM review the current status and suggest or review the plan in @sprint_1.md. Create the specs in specs subdirectory to carry out todays tasks.

**Example Output:**
- specs/day2_spec
