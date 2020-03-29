import { Selector } from 'testcafe';

export default class ExamplePage {
    constructor() {
        this.developer = Selector('#developer-name');
        this.firstCheckbox = Selector('input').withAttribute('name', 'remote');
        this.secondCheckbox = Selector('input').withAttribute('name', 'analysis');
        this.triedTestCafe = Selector('input').withAttribute('name', 'tried-test-cafe');
        this.comments = Selector('textarea').withAttribute('name', 'comments');
        this.name = Selector('#article-header');
    }
}
