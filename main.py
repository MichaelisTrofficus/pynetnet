from __future__ import print_function, unicode_literals

from PyInquirer import style_from_dict, Token, prompt, Separator
from pynetnet.YahooScreener import YahooScreener

style = style_from_dict({
    Token.Separator: '#cc5454',
    Token.QuestionMark: '#673ab7 bold',
    Token.Selected: '#cc5454',  # default
    Token.Pointer: '#673ab7 bold',
    Token.Instruction: '',  # default
    Token.Answer: '#f44336 bold',
    Token.Question: '',
})

questions = [
    {
        'type': 'checkbox',
        'message': 'Select region',
        'name': 'regions',
        'choices': [
            Separator('= Region ='),
            {
                "name": "United States",
                "checked": True,
                "value": "us"
            },
            {
                "name": "Argentina",
                "value": "ar"
            },
            {
                "name": "Australia",
                "value": "au"
            },
            {
                "name": "Bahrain",
                "value": "bh"
            },
            {
                "name": "Canada",
                "value": "ca"
            },
            {
                "name": "Chile",
                "value": "cl"
            },
            {
                "name": "Czech Republic",
                "value": "cz"
            },
            {
                "name": "Denmark",
                "value": "dk"
            },
            {
                "name": "Spain",
                "value": "es"
            },
            {
                "name": "South Africa",
                "value": "za"
            },
            {
                "name": "Venezuela",
                "value": "ve"
            },
            {
                "name": "Taiwan",
                "value": "tw"
            },
            {
                "name": "Tunisia",
                "value": "tn"
            },
            {
                "name": "Thailand",
                "value": "th"
            },
            {
                "name": "Suriname",
                "value": "sr"
            },
            {
                "name": "Sweden",
                "value": "se"
            },
            {
                "name": "Qatar",
                "value": "qa"
            },
            {
                "name": "Poland",
                "value": "pl"
            },
            {
                "name": "Philippines",
                "value": "ph"
            },
            {
                "name": "New Zealand",
                "value": "nz"
            },
            {
                "name": "Netherlands",
                "value": "nl"
            },
            {
                "name": "Mexico",
                "value": "mx"
            },
            {
                "name": "Sri Lanka",
                "value": "lk"
            },
            {
                "name": "South Korea",
                "value": "kr"
            },
            {
                "name": "Jordan",
                "value": "jo"
            },
            {
                "name": "France",
                "value": "fr"
            },
            {
                "name": "Greece",
                "value": "gr"
            },
            {
                "name": "Hungary",
                "value": "hu"
            },
            {
                "name": "Ireland",
                "value": "ie"
            },
            {
                "name": "India",
                "value": "in"
            },
            {
                "name": "Austria",
                "value": "at"
            },
            {
                "name": "Belgium",
                "value": "be"
            },
            {
                "name": "Brazil",
                "value": "br"
            },
            {
                "name": "Switzerland",
                "value": "ch"
            },
            {
                "name": "China",
                "value": "cn"
            },
            {
                "name": "Germany",
                "value": "de"
            },
            {
                "name": "Egypt",
                "value": "eg"
            },
            {
                "name": "Finland",
                "value": "fi"
            },
            {
                "name": "United Kingdom",
                "value": "gb"
            },
            {
                "name": "Hong Kong",
                "value": "hk"
            },
            {
                "name": "Indonesia",
                "value": "id"
            },
            {
                "name": "Israel",
                "value": "il"
            },
            {
                "name": "Italy",
                "value": "it"
            },
            {
                "name": "Japan",
                "value": "jp"
            },
            {
                "name": "Kuwait",
                "value": "kw"
            },
            {
                "name": "Luxembourg",
                "value": "lu"
            },
            {
                "name": "Malaysia",
                "value": "my"
            },
            {
                "name": "Norway",
                "value": "no"
            },
            {
                "name": "Peru",
                "value": "pe"
            },
            {
                "name": "Pakistan",
                "value": "pk"
            },
            {
                "name": "Portugal",
                "value": "pt"
            },
            {
                "name": "Russia",
                "value": "ru"
            },
            {
                "name": "Singapore",
                "value": "sg"
            },
            {
                "name": "French Southern Territories",
                "value": "tf"
            },
            {
                "name": "Timor-Leste",
                "value": "tl"
            },
            {
                "name": "Turkey",
                "value": "tr"
            },
            {
                "name": "Vietnam",
                "value": "vn"
            },
        ],
        'validate': lambda answer: 'You must choose at least one country.' if len(answer) == 0 else True
    }
]

if __name__ == '__main__':
    answers = prompt(questions, style=style)

    ex = YahooScreener(answers['regions'])
    d = ex.get_data()
    print(d)
