<script setup>
import { onMounted, ref } from 'vue'
import { delJSON, getJSON } from '../api'

const items = ref([])
const load = async () => { items.value = (await getJSON('/api/history')).items }
onMounted(load)

const remove = async (id) => {
  await delJSON(`/api/history/${id}`)
  await load()
}
</script>

<template>
  <div class="page"><h1>试算记录</h1>
    <p class="muted">每条记录为锁定快照：途经、站数、票价保持写入时的结果。</p>
    <table>
      <thead><tr><th>#</th><th>时间</th><th>行程</th><th>站数</th><th>票价</th><th></th></tr></thead>
      <tbody>
        <tr v-for="h in items" :key="h.id">
          <td><router-link :to="`/history/${h.id}`">#{{ h.id }}</router-link></td>
          <td>{{ h.created_at }}</td>
          <td>{{ h.input.start }} → {{ h.input.end }}</td>
          <td>{{ h.result.hops ?? '—' }}</td>
          <td>{{ h.result.fare != null ? `¥${h.result.fare}` : '—' }}</td>
          <td><button @click="remove(h.id)">删除</button></td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
