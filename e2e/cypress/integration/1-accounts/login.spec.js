describe('Test Loggin In', () => {
  beforeEach(() => {
    // Set viewport size to widescreen
    cy.viewport('macbook-15')
    
    // Reset the db & create the tables & load all the fixtures
    cy.exec('npm run django:reset_db && npm run django:migrate && npm run django:load_all_fixtures')
    
    // Example commands to load a specific fixture
    //cy.exec('npm run django:load_fixture -- /app/fixtures/testing/003_create_initial_users.json')
  })

  it('redirects to /login', () => {
    cy.visit('/')
    cy.location('href').should('match', /login$/)
  })

  it('403 status without a valid CSRF token', () => {
    // first show that by not providing a valid CSRF token
    // that we will get a 403 status code
    const {email, password} = Cypress.env('client_credentials')
    const headers = { 'X-XSRF-TOKEN': 'invalid-token'}
    const data =  {
      email: email,
      password: password,
      captcha: ''
    }    

    cy.request({
      method: 'POST',
      url: '/login',
      failOnStatusCode: false,
      headers: headers,
      body: data
    }).its('status').should('eq', 403);
  })

  it('Logs as a client user using a valid csrf token', () => {
    const { email, password } = Cypress.env('client_credentials')
    cy.login(email, password)
    cy.visit('/')
    cy.location('href').should('match', /$/)
  })

  it('Log as a manager user using a valid csrf token', () => {
    const { email, password } = Cypress.env('manager_credentials')
    cy.login(email, password)
    cy.visit('/')
    cy.location('href').should('match', /$/)
  })

  it('User logs in with invalid credentials', () => {
    cy.login("dummyuser@test.com", "Pass1234..")
    cy.visit('/')
    cy.location('href').should('match', /login$/)
  })

  it('User logout', () => {
    const { email, password } = Cypress.env('client_credentials')
    cy.login(email, password)
    cy.visit('/')
    cy.location('href').should('match', /$/)
    cy.visit('/logout')
    cy.location('href').should('match', /login$/)
  })
})
