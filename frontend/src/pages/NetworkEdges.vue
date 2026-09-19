<script setup>
import { onMounted, ref } from 'vue'
import { delJSON, getJSON, postJSON } from '../api'
const items = ref([])
const stations = ref([])
const a = ref('')
const b = ref('')
const load = async () => { items.value = (await getJSON('/api/edges')).items }
onMounted(async () => {
  await load()
  stations.value = (await getJSON('/api/stations')).items
})
const add = async () => { await postJSON('/api/edges', { a: a.value, b: b.value }); await load() }
const remove = async (e) => { await delJSON('/api/edges', { a: e.a, b: e.b }); await load() }
</script>
<template>
  <div class="page"><h1>邻接区间</h1>
    <div class="panel">
      <select v-model="a"><option v-for="s in stations" :key="s.code" :value="s.code">{{ s.name }}</option></select>
      —
      <select v-model="b"><option v-for="s in stations" :key="s.code" :value="s.code">{{ s.name }}</option></select>
      <button @click="add">新增边</button>
    </div>
    <table>
      <tbody>
        <tr v-for="(e,i) in items" :key="i">
          <td>{{ e.a }} — {{ e.b }}</td>
          <td><button @click="remove(e)">删除</button></td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
