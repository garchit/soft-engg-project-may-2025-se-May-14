<template>
    <div class="institute-info">
        <h1>INSTITUTES</h1><br><br>
        <table class="institute-table">
            <thead>
                <th>INSTITUTE NAME</th>
                <th>STUDENTS ENROLLED</th>
                <th>ACTIONS</th>
            </thead>
            <tbody>
                <tr v-for="inst in institutes">
                    <td>{{ inst.name}}</td>
                    <td style="text-align: center;">{{ inst.students }}</td>
                    <td>
                      <a href="#" class="text-primary me-2" title="Edit" style="color: black;">
                        <i class="bi bi-pencil-square"></i>
                      </a>
                      <a href="#" class="text-danger me-2" title="Delete" style="color: red; text-shadow: 0 0 1px black;">
                        <i class="bi bi-trash"></i>
                      </a>
                      <a href="#" class="text-warning" title="Block" style="color: yellow">
                        <i class="bi bi-slash-circle"></i>
                      </a>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<script setup>
import { ref } from 'vue'

let institutes = ref([
    { name: 'Institute A', students: 120 },
    { name: 'Institute B', students: 85 },
    { name: 'Institute C', students: 200 }
])


</script>

<style scoped>
h1 {
  font-size: 42px;
  color: white;
}

.institute-info {
  height: 100vh;
  background: linear-gradient(109.62deg, #EFBD7D -1.73%, rgba(244, 123, 123, 0.72) 49.09%, #D99239 91.15%);
  display: flex;
  flex-direction: column;
  align-items: center;
}

.institute-table {
  width: 50%;
  padding: 10px 30px;
  background: rgba(28, 176, 246, 1);
  border: 10px solid rgba(255, 200, 0, 1);
  border-radius: 20px;
  border-collapse: separate;
  border-spacing: 0px 12px;
  color: white;
  font-weight: bold;
  text-align: left;
}

.institute-table thead th {
  padding: 10px 20px;
}


.institute-table tbody tr td {
  background: rgba(66, 66, 66, 0.12);
  padding: 10px 20px;
}

/* Rounded corners on the first and last cell of each row */
.institute-table tbody tr td:first-child {
  border-top-left-radius: 20px;
  border-bottom-left-radius: 20px;
}

.institute-table tbody tr td:last-child {
  border-top-right-radius: 20px;
  border-bottom-right-radius: 20px;
}

/* Hover effect */
.institute-table tbody tr:hover td {
  background: rgba(255, 255, 255, 0.15);
  transition: background 0.3s ease;
}

i{
  font-size: 20px;
  padding: 5px;
}
</style>

