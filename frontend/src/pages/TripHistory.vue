<script setup>
import { onMounted, ref } from 'vue'
import { getJSON } from '../api'
const items = ref([])
onMounted(async () => { items.value = (await getJSON('/api/history')).items })
</script>
<template>
  <div class="page"><h1>试算记录</h1>
    <table>
      <thead><tr><th>#</th><th>时间</th><th>起 → 终</th><th>锁定站数</th><th>锁定票价</th><th></th></tr></thead>
      <tbody>
        <tr v-for="h in items" :key="h.id">
          <td>#{{ h.id }}</td>
          <td>{{ h.created_at }}</td>
          <td>{{ h.start }} → {{ h.end }}</td>
          <td>{{ h.hops }}</td>
          <td>¥{{ h.fare }}</td>
          <td><router-link :to="`/history/${h.id}`">详情</router-link></td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
