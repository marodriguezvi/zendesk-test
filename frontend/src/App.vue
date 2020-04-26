<template>
  <div>
    <header class="bg-light">
    <div class="container">
      <h4 class="py-2">Data viewer</h4>
    </div>
    </header>
   <section class="container mt-3">
      <div class="form-group row">
        <div class="col-md-4">
         <label for="users">Select User</label>
         <select
          id="users"
          class="form-control
          form-control-sm"
          v-model="user">
          <option selected value="">-- All --</option>
          <option
            v-for="user in users"
            :key="user.id"
            :value="user.integration_id">
            {{ user.first_name }} {{ user.last_name }}
          </option>
          </select>
          <label for="search" class="mt-2">Search by ID</label>
          <input
            id="search"
            type="text"
            class="form-control form-control-sm"
            placeholder="Interaction ID"
            v-model="interactionId">
       </div>
       <div class="col-md-8">
          <div class="row">
            <div class="col-md-6">
            <label for="dateFrom">From</label>
            <input
              id="dateFrom"
              type="date"
              class="form-control form-control-sm"
              v-model="dateFrom">
           </div>
           <div class="col-md-6">
              <label for="dateTo">To</label>
              <input
                id="dateTo"
                type="date"
                class="form-control form-control-sm"
                :min="dateFrom"
                v-model="dateTo">
            </div>
         </div>
         <div class="row mt-2">
            <div class="col-md-4">
              <label for="Status">Status</label>
              <select
                id="Status"
                class="form-control
                form-control-sm"
                v-model="status">
                <option selected value="">-- All --</option>
                <option value="new">New</option>
                <option value="open">Open</option>
                <option value="pending">Pending</option>
                <option value="solved">Solved</option>
                <option value="closed">Closed</option>
              </select>
           </div>
           <div class="col-md-4">
              <label for="Priority">Priority</label>
              <select
                id="Priority"
                class="form-control
                form-control-sm"
                v-model="priority">
                <option selected value="">-- All --</option>
                <option value="urgent">Urgent</option>
                <option value="high">High</option>
                <option value="normal">Normal</option>
                <option value="low">Low</option>
              </select>
           </div>
           <div class="col-md-4">
              <label for="Type">Type</label>
              <select
                id="Type"
                class="form-control
                form-control-sm"
                v-model="type">
                <option selected value="">-- All --</option>
                <option value="problem">Problem</option>
                <option value="incident">Incident</option>
                <option value="question">Question</option>
                <option value="task">Task</option>
              </select>
            </div>
          </div>
        </div>
      </div>
      <hr>
        <div class="form-group row">
          <div class="col-md-12 form-group" style="margin-bottom:0px">
          <label class="mr-2">Import</label>
          <button class="btn btn-outline-dark btn-sm mr-2"
            @click="importUsers">Users</button>
          <button class="btn btn-outline-dark btn-sm mr-4"
            @click="importInteractions">Interactions</button>
          <span class="text-muted mr-4">|</span>
          <input
            type="text"
            placeholder="Number of interactions"
            class="form-control form-control-sm d-inline mr-2"
            style="width:29%"
            v-model="numberInteractios">
          <button
            class="btn btn-outline-dark btn-sm mr-4"
            @click="createInteractios">Create interactions</button>
          <span class="text-muted mr-4">|</span>
          <p class="d-inline">Interactions {{ countInteractions }}</p>
        </div>
        <div class="col-md-4 form-group" style="margin-bottom:0px">
        </div>
        </div>
        <hr>
     <div>
        <table class="table mt-4">
          <thead>
            <tr>
              <th scope="col">Full name</th>
              <th scope="col">Integration id</th>
              <th scope="col">Interaction id</th>
              <th scope="col">Status</th>
              <th scope="col">Priority</th>
              <th scope="col">Type</th>
              <th scope="col">Date</th>
            </tr>
          </thead>
          <tbody v-for="ticket in filteredTickets" :key="ticket.id">
            <tr>
              <td>{{ ticket.agent_name }}</td>
              <td>{{ ticket.assignee_id }}</td>
              <td>{{ ticket._id }}</td>
              <td>{{ ticket.status }}</td>
              <td>{{ ticket.priority }}</td>
              <td>{{ ticket.type }}</td>
              <td>{{ ticket.created_at }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>
  </div>
</template>

<script>
export default {
  mounted () {
    this.getUsers()
    this.getInteractions()
  },
  data () {
    return {
      user: '',
      interactionId: '',
      numberInteractios: '',
      dateFrom: '',
      dateTo: '',
      status: '',
      priority: '',
      type: '',
      users: [],
      tickets: []
    }
  },
  computed: {
    filteredTickets () {
      var result = this.tickets.filter(
        (ticket) => ticket.created_at >= this.dateFrom)
      if (this.interactionId) {
        result = this.tickets.filter(
          (ticket) => ticket._id === parseInt(this.interactionId))
      }
      if (this.user) {
        result = result.filter((ticket) => ticket.assignee_id === this.user)
      }
      if (this.dateTo) {
        result = result.filter((ticket) => ticket.created_at <= this.dateTo)
      }
      if (this.status) {
        result = result.filter((ticket) => ticket.status === this.status)
      }
      if (this.priority) {
        result = result.filter((ticket) => ticket.priority === this.priority)
      }
      if (this.type) {
        result = result.filter((ticket) => ticket.type === this.type)
      }
      return result
    },
    countInteractions () {
      return this.filteredTickets.length
    }
  },
  methods: {
    getUsers () {
      this.$http.get('http://localhost:8000/users')
        .then(response => {
          this.users = response.body.users
        }, error => {
          console.log(error)
        })
    },
    getInteractions () {
      this.$http.get('http://localhost:8000/tickets')
        .then(response => {
          this.tickets = response.body.tickets
        }, error => {
          console.log(error)
        })
    },
    importUsers () {
      this.$http.post('http://localhost:8000/import/users')
        .then(response => {
          console.log(response.body)
          this.getUsers()
        }, error => {
          console.log(error)
        })
    },
    importInteractions () {
      this.$http.post('http://localhost:8000/import/tickets')
        .then(response => {
          console.log(response.body)
          this.getInteractions()
        }, error => {
          console.log(error)
        })
    },
    createInteractios () {
      this.$http.post('http://localhost:8000/tickets', { number_tickets:
      this.numberInteractios })
        .then(response => {
          console.log(response.body)
          this.numberInteractios = ''
          this.getInteractions()
        }, error => {
          console.log(error)
        })
    }
  }
}
</script>
