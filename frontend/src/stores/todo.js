import { defineStore } from "pinia";
import axios from "axios";

export const useTodoStore = defineStore("todoStore", {
  state: () => ({
    loading: false,
    error: null,
    todoData: "",
  }),

  actions: {
    async getTodo(arg) {
      let url = ''
      if (arg === 'today') {
        url = "http://127.0.0.1:8000/todo_today/"
      } else {
        url = "http://127.0.0.1:8000/todos/"
      }
      this.loading = true;
      try {
        const response = await axios.get(url, {
          headers: {
            "Content-Type": "application/json",
          },
        });
        // console.log(response)
        if (response.data === null) {
            this.todoData = null;
        } else if (response.status === 500) {
            this.error = response.data;
        } else {
            this.todoData = response.data;
        }
        console.log(this.todoData)
      } catch (error) {
        this.error = error;
        console.error(error);
      } finally {
        this.loading = false;
      }
    },
  },

  getters: {
    getTodos() {
      return this.todoData;
    }
  }
});
