from typing import *
from bs4 import BeautifulSoup, Tag, NavigableString
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
            </head>
            <body>
            </body>
            </html>
        """
        styles: str = """
            <style>
                :root {
                    --fail-button-bg-color: red;
                    --fail-content-bg-color: rgb(255, 120, 120);
                    
                    --pass-button-bg-color: green;
                    --pass-content-bg-color: rgb(120, 255, 120);
                    
                    --pass-body-bg-color: rgb(170, 255, 170);
                    --fail-body-bg-color: rgb(255, 170, 170);
                }
                
                body {
                    margin: 0;
                    font-family: 'Arial', sans-serif;
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
                
                .sub-accordion-content {
                    text-align: center;
                }
                
                .content-part {
                    margin-bottom: 15px;
                }
                
                .content-part-header {
                    font-size: 13px;
                    font-weight: bold;
                }
                
                .content-part-main {
                    font-family: 'Consolas', sans-serif;
                    background-color: white;
                    padding: 7px;
                    display: inline-block;
                    text-align: left;
                }       
            </style>
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
                    <div class="content-part" id="content-first">
                        <div class="content-part-header">INPUT:</div>
                        <div class="content-part-main" id="content-part-main"></div>
                    </div>
                    <div class="content-part" id="content-second">
                        <div class="content-part-header">ACTUAL OUTPUT:</div>
                        <div class="content-part-main" id="content-part-main"></div>
                    </div>
                    <div class="content-part" id="content-third">
                        <div class="content-part-header">PROPER OUTPUT:</div>
                        <div class="content-part-main" id="content-part-main"></div>
                    </div>
                </div>
            </div>
        """

        self.__html_soup: BeautifulSoup = BeautifulSoup(html_innit, 'html.parser')
        self.__styles: BeautifulSoup = BeautifulSoup(styles, 'html.parser')
        self.__html_soup.find('head').append(self.__styles)

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
                testcase_content['style'] = f'background-color: var(--{color}-content-bg-color);'

                in_data: Tag = testcase_content.find(id='content-first').find(id='content-part-main')
                in_data.append(BeautifulSoup(testcase.in_data.replace('\n', '<br>'),
                                             'html.parser'))

                actual_out: Tag = testcase_content.find(id='content-second').find(id='content-part-main')
                actual_out.append(BeautifulSoup(testcase.actual_out.replace('\n', '<br>'),
                                                'html.parser'))

                proper_out: Tag = testcase_content.find(id='content-third').find(id='content-part-main')
                proper_out.append(BeautifulSoup(testcase.actual_out.replace('\n', '<br>'),
                                                'html.parser'))

                testcases_tag.append(new_testcase)

            main_list.append(new_test)

        self.__html_soup.body.append(main_list)
        self.__html_soup.body.append(self.__js_script)

        return self.__html_soup
