<script setup>
import { onMounted, ref } from 'vue'
import { getJSON, putJSON } from '../api'
const items = ref([])
const load = async () => { items.value = (await getJSON('/api/fare-rules')).items }
onMounted(load)
const save = async (r) => {
  const maxHops = (r.max_hops === '' || r.max_hops === undefined) ? null : r.max_hops
  await putJSON(`/api/fare-rules/${r.id}`, { max_hops: maxHops, price: r.price })
  await load()
}
</script>
<template>
  <div class="page"><h1>票价阶梯(按站数)</h1>
    <table>
      <thead><tr><th>最多站数</th><th>票价</th><th></th></tr></thead>
      <tbody>
        <tr v-for="r in items" :key="r.id">
          <td><input type="number" v-model.number="r.max_hops" placeholder="以上" style="width:6rem" /></td>
          <td><input type="number" step="0.01" v-model.number="r.price" style="width:6rem" /></td>
          <td><button @click="save(r)">保存</button></td>
        </tr>
      </tbody>
    </table>
    <p class="muted">改票价表只影响之后的试算；已锁定记录的票价保持快照不变</p>
  </div>
</template>
