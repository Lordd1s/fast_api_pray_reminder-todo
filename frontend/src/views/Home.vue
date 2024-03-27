<template>
    <section>
        <div class="container">
            <div class="title"><i class="fa fa-list" aria-hidden="true"></i><span class="title-text">Задачи на
                    сегодня</span></div>
            <div class="tasks">
                <div class="task" v-if="td.getTodos === null">
                    <span>Нет задачи на сегодня!</span>
                </div>
                <div class="accordion" v-else>
                    <div class="accordion-item" v-for="task in td.getTodos.all_todos" key="task.id">
                        <div class="accordion-header" @click="toggleAccordion(task.id)">{{ task.todo }}</div>
                        <div class="accordion-content" v-show="openAccordion === task.id">
                            {{ task.description }} 
                            <p>{{ task.when_to_do }}</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>
</template>

<script>
import { defineComponent, onMounted } from 'vue';
import { useTodoStore } from '@/stores/todo';
export default defineComponent({
    setup() {
        const todo = useTodoStore();

        onMounted(() => {
            todo.getTodo()
        })

        return { td: todo }
    },

    data() {
        return {
            openAccordion: null
        }
    },

    methods: {
        toggleAccordion(idx) {
            if (this.openAccordion === idx) {
                this.openAccordion = null;
                // console.log(this.openAccordion)
            } else {
                this.openAccordion = idx;
                // console.log(this.openAccordion === idx)


            }
        }
    }
});
</script>

<style scoped>
.container {
    margin: 0 auto;
    padding: 3%;
    width: 40%;
    height: auto;
    background: #ffffff7f;
    display: flex;
    flex-direction: column;
    border-radius: 10px;
    box-shadow: 0 0 5px #fff;
    flex-wrap: nowrap;
    overflow-y: hidden;
}

.title {
    display: flex;
    align-items: center;
    gap: 5%;
    font-size: clamp(1em, 2.5rem, 3rem);
}

.title-text {
    font-size: clamp(10px, 2.5rem, 3rem);
    font-family: 'Raleway', sans-serif;
    font-weight: 300;
    background: linear-gradient(45deg, #4a4a4a, #8b208f);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.tasks {
    margin-top: 34px;
}

.accordion-item {
  border: 1px solid #ccc;
  margin-bottom: 5px;
}

.accordion-header {
  background-color: #f4f4f4;
  padding: 10px;
  cursor: pointer;
}

.accordion-content {
  padding: 10px;
}
</style>