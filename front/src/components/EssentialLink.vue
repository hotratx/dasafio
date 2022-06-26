<template>
  <div v-for="item in props.data" :key="item.title">
    <q-item
      v-if="onlyStaff(item.title)"
      :active="llink === item.title"
      @click="llink = item.title"
      clickable
      :to="{ name: item.routeName }"
    >
      <q-item-section
        class="col-3"
        v-if="item.icon"
        avatar
      >
        <q-icon :name="item.icon" />
      </q-item-section>

      <q-item-section class="col-9">
        <q-item-label>{{ item.title }}</q-item-label>
        <q-item-label caption>
        </q-item-label>
      </q-item-section>
    </q-item>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useAuth } from 'stores/userAuth'

const store = useAuth()

interface ILink {
  title: string
  icon: string
  routeName?: string
  caption?: string
}

let llink = ref('Home')

const onlyStaff = (name: string): boolean => {
  if (name == 'Admin' || name == 'Alunos') {
    if (store.user.type_user === 'staff' || store.user.type_user === 'professor') {
      return true
    } else {
      return false
    }
  }
  return true
}


const props = defineProps<{
  data: ILink[]
}>()

</script>

<style lang="scss">
.border-black {
  border: 1px;
}

.my-menu-link {
  color: green;
  background: #F2C037;
}
</style>
