<script setup>
import { onMounted, ref } from 'vue'
import { delJSON, getJSON, postJSON, putJSON } from '../api'

const items = ref([])
const newMax = ref(null)
const newPrice = ref(null)
const editId = ref(null)
const editMax = ref(null)
const editPrice = ref(null)

const load = async () => { items.value = (await getJSON('/api/fare-rules')).items }
onMounted(load)

const add = async () => {
  await postJSON('/api/fare-rules', { max_hops: newMax.value === '' || newMax.value == null ? null : Number(newMax.value), price: Number(newPrice.value) })
  newMax.value = null; newPrice.value = null
  await load()
}

const startEdit = (r) => { editId.value = r.id; editMax.value = r.max_hops; editPrice.value = r.price }
const save = async () => {
  await putJSON(`/api/fare-rules/${editId.value}`, { max_hops: editMax.value === '' || editMax.value == null ? null : Number(editMax.value), price: Number(editPrice.value) })
  editId.value = null
  await load()
}

const remove = async (id) => { await delJSON(`/api/fare-rules/${id}`); await load() }
</script>

<template>
  <div class="page"><h1>票价阶梯(按站数)</h1>
    <table>
      <thead><tr><th>最多站数</th><th>票价</th><th></th></tr></thead>
      <tbody>
        <tr v-for="r in items" :key="r.id">
          <template v-if="editId === r.id">
            <td><input type="number" v-model="editMax" placeholder="留空=以上" /></td>
            <td><input type="number" step="0.01" v-model="editPrice" /></td>
            <td><button @click="save">保存</button></td>
          </template>
          <template v-else>
            <td>{{ r.max_hops ?? '以上' }}</td>
            <td>{{ r.price }}</td>
            <td>
              <button @click="startEdit(r)">改</button>
              <button @click="remove(r.id)">删</button>
            </td>
          </template>
        </tr>
      </tbody>
    </table>
    <div class="panel">
      <input type="number" v-model="newMax" placeholder="最多站数(留空=以上)" />
      <input type="number" step="0.01" v-model="newPrice" placeholder="票价" />
      <button @click="add">新增规则</button>
    </div>
  </div>
</template>

<style scoped>
button + button { margin-left: 0.4rem; }
input { margin-right: 0.4rem; }
</style>
