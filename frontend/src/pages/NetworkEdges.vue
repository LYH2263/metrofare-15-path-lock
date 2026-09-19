<script setup>
import { onMounted, ref } from 'vue'
import { delJSON, getJSON, postJSON } from '../api'

const items = ref([])
const stations = ref([])
const a = ref('')
const b = ref('')
const error = ref('')

const load = async () => {
  const [e, s] = await Promise.all([getJSON('/api/edges'), getJSON('/api/stations')])
  items.value = e.items
  stations.value = s.items
}
onMounted(load)

const add = async () => {
  error.value = ''
  try {
    await postJSON('/api/edges', { a: a.value, b: b.value })
    await load()
  } catch (e) { error.value = String(e) }
}

const remove = async (x, y) => {
  await delJSON(`/api/edges?a=${encodeURIComponent(x)}&b=${encodeURIComponent(y)}`)
  await load()
}
</script>

<template>
  <div class="page"><h1>邻接区间</h1>
    <div class="panel">
      <select v-model="a"><option v-for="s in stations" :key="s.code" :value="s.code">{{ s.name }}</option></select>
      —
      <select v-model="b"><option v-for="s in stations" :key="s.code" :value="s.code">{{ s.name }}</option></select>
      <button @click="add">新增区间</button>
      <p v-if="error" class="muted">{{ error }}</p>
    </div>
    <table>
      <tbody>
        <tr v-for="(e, i) in items" :key="i">
          <td>{{ e.a }} — {{ e.b }}</td>
          <td><button @click="remove(e.a, e.b)">删除</button></td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
