Cypress.Commands.add('login', (email, password) => {
    cy.log("Executing Comand Login....")
    
    // First step, we extract the csrf token from the login html template
    cy.visit("/login");
    cy.get("[name=csrfmiddlewaretoken]")
    .should("exist")
    .should("have.attr", "value")
    .as("csrfToken")
    
    // Second step, now that we have the perform the login steps
    cy.get("@csrfToken").then((csrfToken) => {
      // Set request data and headers
      const headers = { 'X-XSRF-TOKEN': csrfToken}
      const data =  {
        email: email,
        password: password,
        captcha: ''
      }
  
      // Perform login POST request
      cy.request({
        method: 'POST',
        url: '/login',
        failOnStatusCode: false,
        headers: headers,
        body: data
      }).its('status').should('eq', 200);
  
      cy.visit('/')
      cy.location('href').should('match', /$/)
    })
  })