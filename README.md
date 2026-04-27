# What?

Lament is a ready-to-use, highly customizable injection toolkit for launching supply chain attacks against any python(PyPI) package, with the most advanced and common attack vectors.

You can create a compromised version of a package with this toolkit within minutes.

# Wait, What??

Let's say, you want to compromise the `requests` package. You can use Lament to create a compromised version of the package with the following steps:

1. Install Lament using pip: `pip install Lament`
2. Create a new directory for your compromised package: `mkdir compromised_requests`
3. Navigate to the directory: `cd compromised_requests`
4. Type `Lament .` to move into the interactive menu, and customize your version of the poisoned `requests` (You need to install requirements.txt first, but the toolkit will automatically do it for you if you don't have them)
5. Publish it through PyPI, by using a name like `reqeust` or what, or...... (you know what to do, don't you, you asshole huh?)

And that's it! You can now cook a poisoned version of the `requests` package within a few minutes, through the lament toolkit.


