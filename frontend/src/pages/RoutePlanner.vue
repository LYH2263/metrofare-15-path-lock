<script setup>
import { computed, onMounted, ref } from 'vue'
import { getJSON, postJSON } from '../api'

const stations = ref([])
const start = ref('A1')
const end = ref('B2')
const out = ref(null)
const savedId = ref(null)

onMounted(async () => { stations.value = (await getJSON('/api/stations')).items })

const names = computed(() => Object.fromEntries(stations.value.map(s => [s.code, s.name])))
const label = (code) => (names.value[code] ? `${code} ${names.value[code]}` : code)

// Both actions recompute against the CURRENT graph; only "保存" locks a snapshot record.
const run = async (persist) => {
  out.value = await postJSON('/api/quote', { start: start.value, end: end.value, persist })
  savedId.value = persist ? out.value.run_id : null
}
</script>

<template>
  <div class="page"><h1>最短站数票价</h1>
    <div class="panel">
      <select v-model="start"><option v-for="s in stations" :key="s.code" :value="s.code">{{ s.name }}</option></select>
      →
      <select v-model="end"><option v-for="s in stations" :key="s.code" :value="s.code">{{ s.name }}</option></select>
      <button @click="run(false)">只读试算</button>
      <button @click="run(true)">试算并保存</button>
    </div>
    <div v-if="out" class="panel">
      <p class="muted">当前图试算结果{{ savedId ? ` · 已锁定为记录 #${savedId}` : ' · 未保存' }}</p>
      <template v-if="out.reachable">
        <p class="path">
          <template v-for="(code, i) in out.path" :key="i">
            <span v-if="i"> → </span><span class="stop">{{ label(code) }}</span>
          </template>
        </p>
        <p>站数 {{ out.hops }} · 票价 <span class="hero-num">¥{{ out.fare }}</span></p>
      </template>
      <p v-else class="muted">不可达</p>
    </div>
  </div>
</template>

<style scoped>
.path { line-height: 1.9; }
.stop { white-space: nowrap; }
button + button { margin-left: 0.5rem; }
</style>
