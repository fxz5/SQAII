import { Selector, t } from 'testcafe';
import LoginPage from '../page_model/example_page'
const data = require('./config.json');

fixture `Instagram Login`
    .page `https://www.instagram.com/`;

const ex_page = new LoginPage();
const fs = require('fs');

test('Log in test', async t => {
    await t
    .typeText(ex_page.username, data['username'])
    .typeText(ex_page.password, data['password'])
    .wait(2000) 
    .click(ex_page.submitButton)
    .wait(5000) 
});