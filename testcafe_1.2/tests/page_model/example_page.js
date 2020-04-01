import { Selector } from 'testcafe';

export default class LoginPage {
    constructor() {
        this.username = Selector('input').withAttribute('name', 'username');
        this.password = Selector('input').withAttribute('name', 'password');
        this.submitButton = Selector('button').withAttribute('type', 'submit');
    }
}
