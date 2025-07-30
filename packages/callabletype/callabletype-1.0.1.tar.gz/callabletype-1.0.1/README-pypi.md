<a name="readme-top"></a>

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]







<!-- About -->
<div align="center">

<h3 align="center">Python CallableType</h3>

<p align="center">

Specialized types for callable objects in Python.

[Changelog][changelog-url] · [Report Bug][issues-url] · [Request Feature][issues-url]
 
</p>

</div>



<!-- ABOUT THE PROJECT -->

##  About The Project

Python 3.x provides customized callable types.

How can we distinguish between types like class, function, and method? You might think of using the `types` or `inspect` modules as a solution. However, these traditional types can be a bit confusing. Especially when it comes to distinguishing between function and method types, you'll notice that `types.FunctionType` does not cover `types.MethodType`. For this reason, callable types have been redefined using this library.




###  Built With

* [![python-shield][python-shield]][pypi-project-url]

<br>


<!-- GETTING STARTED -->

##  Getting Started

To get a local copy up and running follow these simple example steps.

###  Prerequisites

Does not require any prerequisites

###  Installation

1. Clone the repo
```sh
git clone https://github.com/TahsinCr/python-callabletype.git
```

2. Install PIP packages
```sh
pip install callabletype
```


<br>



<!-- USAGE EXAMPLES -->

##  Usage

We have a class named `Parrot(name, color, age)` that includes a method `walk(self)`. Additionally, there is a function called `parrot_fly()`. We can choose and control the types of these functions in detail.
```python
from callabletype import (
    get_callable_type, is_function, CLASS, FUNCTION, METHOD, SELFMETHOD, INSTANCESELFMETHOD
)

class Parrot:
    def __init__(self, name:str, color:str, age:int):
        self.name = name
        self.color = color
        self.age = age
    
    def walk(self):
        print("The parrot named {} walked".format(self.name))
    
def parrot_fly(parrot:Parrot):
    print("The parrot named {} flew".format(parrot.name))

parrot = Parrot(name='Kiwi', color='green', age=14)

objects = {
    'function' : parrot_fly,
    'class' : Parrot,
    'method' : Parrot.walk,
    'self-method' : Parrot.walk,
    'instance-self-method' : parrot.walk
}

for type_name, object in objects.items():
    type = get_callable_type(object)
    check_function = is_function(object)
    check_method = type in METHOD
    check_class = CLASS.check_func(object)
    print("'{}' : {} (result_type={}, is_function={}, is_method={}, is_class={})\n".format(
        object, type_name, type, check_function, check_method, check_class
    ))

```
Output
```
'<function parrot_fly at 0x000001D8C23F3EC0>' : function (result_type=FUNCTION, is_function=True, is_method=False, is_class=False)

'<class '__main__.Parrot'>' : class (result_type=CLASS, is_function=False, is_method=False, is_class=True)

'<function Parrot.walk at 0x000001D8C25B1260>' : method (result_type=SELFMETHOD, is_function=True, is_method=True, is_class=False)

'<function Parrot.walk at 0x000001D8C25B1260>' : self-method (result_type=SELFMETHOD, is_function=True, is_method=True, is_class=False)

'<bound method Parrot.walk of <__main__.Parrot object at 0x000001D8C2455BE0>>' : instance-self-method (result_type=INSTANCESELFMETHOD, is_function=True, is_method=True, is_class=False)
```

_For more examples, please refer to the [Documentation][wiki-url]_

<br>





<!-- LICENSE -->

##  License

Distributed under the MIT License. See [LICENSE][license-url] for more information.


<br>





<!-- CONTACT -->

##  Contact

Tahsin Çirkin - [@TahsinCrs][x-url] - TahsinCr@outlook.com

Project: [TahsinCr/python-callabletype][project-url]







<!-- IMAGES URL -->

[python-shield]: https://img.shields.io/pypi/pyversions/callabletype?style=flat-square

[contributors-shield]: https://img.shields.io/github/contributors/TahsinCr/python-callabletype.svg?style=for-the-badge

[forks-shield]: https://img.shields.io/github/forks/TahsinCr/python-callabletype.svg?style=for-the-badge

[stars-shield]: https://img.shields.io/github/stars/TahsinCr/python-callabletype.svg?style=for-the-badge

[issues-shield]: https://img.shields.io/github/issues/TahsinCr/python-callabletype.svg?style=for-the-badge

[license-shield]: https://img.shields.io/github/license/TahsinCr/python-callabletype.svg?style=for-the-badge

[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555



<!-- Github Project URL -->

[project-url]: https://github.com/TahsinCr/python-callabletype

[pypi-project-url]: https://pypi.org/project/callabletype

[contributors-url]: https://github.com/TahsinCr/python-callabletype/graphs/contributors

[stars-url]: https://github.com/TahsinCr/python-callabletype/stargazers

[forks-url]: https://github.com/TahsinCr/python-callabletype/network/members

[issues-url]: https://github.com/TahsinCr/python-callabletype/issues

[wiki-url]: https://github.com/TahsinCr/python-callabletype/wiki

[license-url]: https://github.com/TahsinCr/python-callabletype/blob/master/LICENSE

[changelog-url]:https://github.com/TahsinCr/python-callabletype/blob/master/CHANGELOG.md



<!-- Contacts URL -->

[linkedin-url]: https://linkedin.com/in/TahsinCr

[x-url]: https://twitter.com/TahsinCrs
