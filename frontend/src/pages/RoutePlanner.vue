<script setup>
import { onMounted, ref } from 'vue'
import { getJSON, postJSON } from '../api'
const stations = ref([])
const start = ref('A1')
const end = ref('B2')
const out = ref(null)
const lockedId = ref(null)
onMounted(async () => { stations.value = (await getJSON('/api/stations')).items })
const quote = async (persist) => {
  lockedId.value = null
  out.value = await postJSON('/api/quote', { start: start.value, end: end.value, persist })
  if (persist) lockedId.value = out.value.run_id
}
</script>
<template>
  <div class="page"><h1>最短站数票价</h1>
    <div class="panel">
      <select v-model="start"><option v-for="s in stations" :key="s.code" :value="s.code">{{ s.name }}</option></select>
      →
      <select v-model="end"><option v-for="s in stations" :key="s.code" :value="s.code">{{ s.name }}</option></select>
      <button @click="quote(false)">只读试算</button>
      <button @click="quote(true)">试算并锁定记录</button>
    </div>
    <div v-if="out" class="panel">
      <template v-if="out.reachable">
        <p>当前途经：{{ out.path.join(' → ') }}</p>
        <p>站数 {{ out.hops }} · 票价 <span class="hero-num">¥{{ out.fare }}</span></p>
        <p v-if="lockedId" class="muted">已锁定为记录 #{{ lockedId }}：途经/站数/票价已快照，之后增删边、改票价表不影响该记录</p>
        <p v-else class="muted">只读试算 · 按当前图实时计算，未写入记录</p>
      </template>
      <p v-else class="muted">不可达</p>
    </div>
  </div>
</template>
