# Daily Updates

## Required

1. What is the branch you worked on (has to be pushed to the repo)?
2. What is the progress so far?
3. Any difficulties?
4. What is the plan for the days before the deadline?

## Team Members:
### Kanchan
Nov 22
1. backend_dev 
2. The initial function for booking has been completed.
3. It was difficult to piece together what's needed to make a booking, what gets changed, and how to reflect that in the database.
4. Discuss with my group to see if any adjustments are needed for the booking function

### Shuvi
1. Initial commit
2. Added test cases to test_models.py
3. Added address field for create_listing
4. Moved test cases to injection_tests.py
5. Addressed PR comments
6. Added address to create_listing

### Andrew
Nov 16
1. register_injection
2. made outline for register sql injection test cases (no test cases are complete, but I've got a good idea of what I want to do)
3. Don't know exactly what to test to ensure the attack wasn't successful.
4. Ask TA for clarification on SQL Injection, and use that to complete test cases.

Nov 17
1. register_injection
2. Finished register injection test cases.
3. No
4. I'm done my section, I just need to review other people's PR's, and assist others as necessary.

### Kaz
Branched worked on
* frontend_dev

Progress so far
* injection_tests.py
  * Created injection tests for 1/2 of create_listing function
    * Parameters: title, description, price
* listing.py
  * Fixed regex to properly validate titles
* test_frondend.py
  * Refactored teammate's code to reduce smelly code
* Generic_SQLI.txt
  * Added file for Injection lines

Difficulties
* .hmtl
  * Wasn't very familiar with HTML which forced me to learn a lot of things very quick
  * 


Next steps
* Looking at existing code to see if any other instances can be refactored
* Improving UI/UX
  * Giving better error messages
  * Limiting input
* Adding new features
  * Deleting Listings/Making them unavailable
* Resolve merge conflicts when merging into main
