from typing import *
from bs4 import BeautifulSoup, Tag
from copy import copy
from test import Test
from testcase import Testcase


class HTMLGenerator:
    def __init__(self, tests: List[Test]) -> None:
        self.__tests: List[Test] = tests

        html_innit: str = """
            <!DOCTYPE html>
            <html lang="pl">
            <head>
                <meta charset="UTF-8">
                <title></title>
                <style>
                    :root {
                        --fail-button-bg-color: red;
                        --fail-content-bg-color: rgba(255, 102, 102, 0.8);
                        
                        --pass-button-bg-color: green;
                        --pass-content-bg-color: rgba(144, 238, 144, 0.8);
                        
                        --pass-body-bg-color: rgb(200, 255, 200);
                        --fail-body-bg-color: rgb(255, 200, 200);
                    }
                    
                    body {
                        margin: 0;
                    }
                    
                    .accordion {
                        width: 100vw;
                    }
                    
                    .accordion-item {
                        margin: 10px 0;
                    }
                    
                    .accordion-item:first-child {
                        margin: 0;
                    }
                    
                    .accordion-button, .sub-accordion-button {
                        background-color: var(--fail-button-bg-color);
                        border: none;
                        width: 100%;
                        text-align: left;
                        padding: 10px 0;
                        cursor: pointer;
                        outline: none;
                        text-align: center;
                    }
                    
                    .accordion-button {
                        font-size: 25px;
                        font-weight: bold;
                    }
                    
                    .sub-accordion-button {
                        font-size: 15px;
                        font-weight: bold;
                    }
            
                    .accordion-content, .sub-accordion-content {
                        display: none;
                        padding: 5px 10px;
                    }
            
                    .sub-accordion-content div {
                        padding: 5px 0;
                    }
                </style>
            </head>
            <body>
            </body>
            </html>
        """
        js_script: str = """
            <script>
                document.querySelectorAll('.accordion-button, .sub-accordion-button').forEach(button => {
                    button.addEventListener('click', function() {
                        let content = this.nextElementSibling;
                        
                        if (content.style.display === "block") {
                            content.querySelectorAll(".sub-accordion-content").forEach(function (item) {
                                item.style.display = "none";
                            });
                            
                            content.style.display = "none";
                            
                        } else {
                            content.style.display = "block";
                        }
                    });
                });
            </script>
        """
        test_tag: str = """
            <div class="accordion-item">
                <button class="accordion-button" id="test-button"></button>
                    <div class="accordion-content">
                        <div class="sub-accordion" id="testcases">
                        </div>
                    </div>
            </div>
        """
        testcase_tag: str = """
            <div class="sub-accordion-item">
                <button class="sub-accordion-button" id="testcase-button"></button>
                <div class="sub-accordion-content" id="testcase-content">
                </div>
            </div>
        """

        self.__html_soup: BeautifulSoup = BeautifulSoup(html_innit, 'html.parser')
        self.__js_script: BeautifulSoup = BeautifulSoup(js_script, 'html.parser')
        self.__test_tag: BeautifulSoup = BeautifulSoup(test_tag, 'html.parser')
        self.__testcase_tag: BeautifulSoup = BeautifulSoup(testcase_tag, 'html.parser')

    def generateResults(self) -> BeautifulSoup:
        body_tag: Tag = self.__html_soup.find('body')
        if all(i.passed for i in self.__tests):
            body_tag['style'] = 'background-color: var(--pass-body-bg-color);'
        else:
            body_tag['style'] = 'background-color: var(--fail-body-bg-color);'

        main_list: Tag = self.__html_soup.new_tag('div')
        main_list['class'] = main_list['id'] = 'accordion'

        test: Test
        for test in self.__tests:
            new_test: Tag = copy(self.__test_tag)
            test_button: Tag = new_test.find(id='test-button')
            test_button.string = test.name

            if test.passed:
                test_button['style'] = 'background-color: var(--pass-button-bg-color);'
            else:
                test_button['style'] = 'background-color: var(--fail-button-bg-color);'

            testcases_tag: Tag = new_test.find(id='testcases')

            testcase: Testcase
            for testcase in test.testcases:
                new_testcase: Tag = copy(self.__testcase_tag)
                testcase_button: Tag = new_testcase.find(id='testcase-button')
                testcase_button.string = testcase.name

                color: str = 'pass' if testcase.passed else 'fail'

                if testcase.passed:
                    testcase_button['style'] = f'background-color: var(--{color}-button-bg-color);'
                else:
                    testcase_button['style'] = f'background-color: var(--{color}-button-bg-color);'

                testcase_content: Tag = new_testcase.find(id='testcase-content')

                in_data: Tag = self.__html_soup.new_tag('div')
                in_data['style'] = f'background-color: var(--{color}-content-bg-color);'
                in_data.string = testcase.in_data
                testcase_content.append(in_data)

                out_data: Tag = self.__html_soup.new_tag('div')
                out_data['style'] = f'background-color: var(--{color}-content-bg-color);'
                out_data.string = testcase.out_data
                testcase_content.append(out_data)

                actual_data: Tag = self.__html_soup.new_tag('div')
                actual_data['style'] = f'background-color: var(--{color}-content-bg-color);'
                actual_data.string = testcase.actual_out
                testcase_content.append(actual_data)

                testcases_tag.append(new_testcase)

            main_list.append(new_test)

        self.__html_soup.body.append(main_list)
        self.__html_soup.body.append(self.__js_script)

        return self.__html_soup
