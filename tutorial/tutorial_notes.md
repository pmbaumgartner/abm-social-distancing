# Tutorial Notes

1. How do users get the requirements.txt
2. `MoneyModel.py` - is the casing correct following coding standards for python files?
3. Comer2014 - Citation link is broken. https://mesa.readthedocs.io/en/master/tutorials/intro_tutorial.html#comer2014 - http://gradworks.umi.com/36/23/3623940.html
4. "Every agent is expected to have a step method, which takes a model object as its only argument" - this part could use some better sequencing. Maybe make the exercise build off of printing the unique id.
5. "You’ll probably see something like the distribution shown below. " - plot is actually above this part in the narrative.
6. `moore` argument to `get_neighborhood` - unclear what this does for new users. Could be `diagonal`?
7. `give_money` - other agent is now called `other`, but is called `other_agent` in the `step` method
8. "Now, putting that all together should look like this:" - switched definition of `MoneyModel` and `MoneyAgent`
9. `from mesa.batchrunner import BatchRunner` gets imported, but not used in the next code block. Wait to import until the block of code that executes the model.
10. Do not import `compute_gini` in the batch runner script.