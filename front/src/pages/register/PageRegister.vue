<template>
  <q-layout>
    <q-page-container>
      <q-page class="flex flex-center">
        <div
          id="particles-js"
          :class="$q.dark.isActive ? 'dark_gradient' : 'normal_gradient'"
        ></div>
        <q-btn
          color="white"
          class="absolute-top-right"
          flat
          round
          @click="$q.dark.toggle()"
          :icon="$q.dark.isActive ? 'nights_stay' : 'wb_sunny'"
        />
        <q-card
          class="login-form"
          v-bind:style="
            $q.platform.is.mobile ? { width: '80%' } : { width: '30%' }
          "
        >
          <q-img src="/statics/images/pharmacy.jpg"></q-img>
          <q-card-section>
            <q-avatar
              size="74px"
              class="absolute"
              style="top: 0;right: 25px;transform: translateY(-50%);"
            >
              <img src="https://cdn.quasar.dev/img/boy-avatar.png" />
            </q-avatar>
            <div class="row no-wrap items-center">
              <div class="col text-h6 ellipsis">
                Registrar
              </div>
            </div>
          </q-card-section>
          <q-card-section>
            <q-form class="q-gutter-md" @submit.prevent="handleRegister">
              <q-input 
                filled 
                v-model="form.username" 
                label="Username" 
                lazy-rules 
                :rules="[val => val.length > 0 || 'Username é requerido']"
              >
               <template v-slot:prepend>
                <q-icon name="mdi-account" />
              </template>
              </q-input>

              <q-input 
                filled 
                v-model="form.email" 
                label="Email" 
                lazy-rules 
                :rules="[val => isEmail(val) || 'Email é requerido']"
              >
               <template v-slot:prepend>
                <q-icon name="mdi-email" />
              </template>
              </q-input>

              <q-input
                type="password"
                filled
                v-model="form.password"
                label="Password"
                lazy-rules
                :rules="[val => val.length > 0 || 'Password requerido']"
              >
               <template v-slot:prepend>
                <q-icon name="mdi-lock" />
              </template>
              </q-input>



              <div class="row q-ma-md justify-center">
                <q-btn
                  class="full-width"
                  label="Login"
                  type="submit"
                  color="primary"
                />

              <div style="margin-top: 20px">
                <span class="justify-center"> Já possui uma conta? </span>
                <router-link class="link" :to="'/login'">Login</router-link>
              </div>

              <div>
                <span class="justify-center"> Perder a senha? </span>
                <router-link class="link" :to="'/home'">Reset senha</router-link>
              </div>
              </div>
            </q-form>
          </q-card-section>
        </q-card>
      </q-page>
    </q-page-container>
  </q-layout>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ICredentials } from 'components/models'
import { useAuth } from 'stores/userAuth'
import isEmail from 'src/composables/typeCheck'

const router = useRouter()
const store = useAuth()

const form = ref<ICredentials>({
  email: '',
  password: '',
  username: ''
})

const handleRegister = async () => {
  try {
    await store.register(form.value)
    await router.push({
      name: 'confirm-email',
    })
  } catch (error) {
    console.log('error no Login', error)
  }
}

onMounted(() => {
  particlesJS('particles-js', {
    'particles': {
        'number': {
            'value': 80,
            'density': {
                'enable': true,
                'value_area': 800
            }
        },
        'color': {
            'value': '#ffffff'
        },
        'shape': {
            'type': 'circle',
            'stroke': {
                'width': 0,
                'color': '#000000'
            },
            'polygon': {
                'nb_sides': 5
            },
            'image': {
                'src': 'img/github.svg',
                'width': 100,
                'height': 100
            }
        },
        'opacity': {
            'value': 0.5,
            'random': false,
            'anim': {
                'enable': false,
                'speed': 1,
                'opacity_min': 0.1,
                'sync': false
            }
        },
        'size': {
            'value': 3,
            'random': true,
            'anim': {
                'enable': false,
                'speed': 40,
                'size_min': 0.1,
                'sync': false
            }
        },
        'line_linked': {
            'enable': true,
            'distance': 150,
            'color': '#ffffff',
            'opacity': 0.4,
            'width': 1
        },
        'move': {
            'enable': true,
            'speed': 6,
            'direction': 'none',
            'random': false,
            'straight': false,
            'out_mode': 'out',
            'bounce': false,
            'attract': {
                'enable': false,
                'rotateX': 600,
                'rotateY': 1200
            }
        }
    },
    'interactivity': {
        'detect_on': 'canvas',
        'events': {
            'onhover': {
                'enable': true,
                'mode': 'grab'
            },
            'onclick': {
                'enable': true,
                'mode': 'push'
            },
            'resize': true
        },
        'modes': {
            'grab': {
                'distance': 140,
                'line_linked': {
                    'opacity': 1
                }
            },
            'bubble': {
                'distance': 400,
                'size': 40,
                'duration': 2,
                'opacity': 8,
                'speed': 3
            },
            'repulse': {
                'distance': 200,
                'duration': 0.4
            },
            'push': {
                'particles_nb': 4
            },
            'remove': {
                'particles_nb': 2
            }
        }
    },
    'retina_detect': true
  });
})
</script>


<style lang="scss">
#particles-js {
  position: absolute;
  width: 100%;
  height: 100%;
  background-repeat: no-repeat;
  background-size: cover;
  background-position: 50% 50%;
}
.normal_gradient {
  background: linear-gradient(145deg, rgb(74, 94, 137) 15%, #b61924 70%);
}
.dark_gradient {
  background: linear-gradient(145deg, rgb(11, 26, 61) 15%, #4c1014 70%);
}
.login-form {
  position: absolute;
}
.link {
  color: $primary;
  text-decoration: none;
  font-weight: 500;
  font-size: .75rem;
  &:hover {
    color: #000;
  }
}
</style>
