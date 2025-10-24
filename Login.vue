<!-- filepath: src/components/Login.vue -->
<template>
  <div class="login">
    <div v-if="mountedText" class="mounted-text">{{ mountedText }}</div>
    <h2>Register</h2>
    <form @submit.prevent="register">
      <input v-model="regUsername" placeholder="Username" required />
      <input v-model="regEmail" placeholder="Email" required type="email" />
      <input v-model="regPassword" type="password" placeholder="Password" required />
      <button type="submit">Register</button>
    </form>
    <p v-if="registerMsg" :class="{'error': registerMsg.includes('Error') || registerMsg.includes('failed') || registerMsg.includes('already'), 'success': !registerMsg.includes('Error') && !registerMsg.includes('failed') && !registerMsg.includes('already')}">{{ registerMsg }}</p>

    <h2>Login</h2>
    <form @submit.prevent="login">
      <input v-model="username" placeholder="Username" required />
      <input v-model="password" type="password" placeholder="Password" required />
      <button type="submit">Login</button>
    </form>
    <p v-if="loginSuccessMsg" class="success">{{ loginSuccessMsg }}</p>
    <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Login',
  data() {
    return {
      regUsername: '',
      regEmail: '',
      regPassword: '',
      registerMsg: '',
      username: '',
      password: '',
      errorMessage: '',
      mountedText: '',
      loginSuccessMsg: ''
    };
  },
  async mounted() {
    try {
      const res = await axios.get('http://localhost:9000');
      this.mountedText = typeof res.data === 'string' ? res.data : (res.data.message || JSON.stringify(res.data));
    } catch (e) {
      console.error('Mounted fetch error:', e);
      this.mountedText = 'Could not fetch from backend';
    }
  },
  methods: {
    async register() {
      try {
        const res = await axios.post('http://localhost:9000/register', {
          username: this.regUsername,
          email: this.regEmail,
          password: this.regPassword
        }, {
          headers: { 'Content-Type': 'application/json' }
        });
        this.registerMsg = res.data.message;
        this.regUsername = '';
        this.regEmail = '';
        this.regPassword = '';
      } catch (err) {
        console.error('Registration error details:', {
          message: err.message,
          response: err.response ? err.response.data : 'No response',
          status: err.response ? err.response.status : 'No status',
          config: err.config ? err.config.url : 'No config'
        });
        const resp = err.response && err.response.data;
        if (resp) {
          if (Array.isArray(resp.detail)) {
            this.registerMsg = resp.detail.map(d => d.msg || JSON.stringify(d)).join('; ');
          } else if (resp.detail) {
            this.registerMsg = resp.detail;
          } else {
            this.registerMsg = JSON.stringify(resp);
          }
        } else {
          this.registerMsg = 'Network Error: Could not connect to backend. Check console for details.';
        }
      }
    },
    async login() {
      try {
        const response = await axios.post('/api/login', {
          username: this.username,
          password: this.password
        }, {
          headers: { 'Content-Type': 'application/json' }
        });
        this.errorMessage = '';
        this.loginSuccessMsg = response.data && response.data.message ? response.data.message : 'Login successful!';
        this.username = '';
        this.password = '';
      } catch (error) {
        console.error('Login error details:', {
          message: error.message,
          response: error.response ? error.response.data : 'No response',
          status: error.response ? error.response.status : 'No status',
          config: error.config ? error.config.url : 'No config'
        });
        this.errorMessage = (error.response && error.response.data && error.response.data.detail) ? error.response.data.detail : 'Invalid username or password';
      }
    }
  }
}
</script>

<style scoped>
.login {
  max-width: 300px;
  margin: auto;
  padding: 1em;
  border: 1px solid #ccc;
  border-radius: 5px;
}
.error {
  color: red;
}
.success {
  color: green;
}
.mounted-text {
  margin-bottom: 1em;
  font-weight: bold;
  color: #333;
}
</style>