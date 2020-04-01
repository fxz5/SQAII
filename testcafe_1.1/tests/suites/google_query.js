import { Selector, t } from 'testcafe';
import ExamplePage from '../page_model/example_page'

fixture `Getting Started`
    .page `http://devexpress.github.io/testcafe/example`;

const ex_page = new ExamplePage();

test('My example test', async t => {
    const name = 'Luis';
    await t
        .typeText(ex_page.developer, name)
        .click(ex_page.firstCheckbox)
        .click(ex_page.secondCheckbox)
        .click(ex_page.triedTestCafe)
        .typeText(ex_page.comments, 'TestCafe is a very flexible and neaty framework!')
        .click('#submit-button')
        .wait(2000)

    await t
    .expect(ex_page.name.innerText).contains(name)
    .wait(1000)
        
        
});