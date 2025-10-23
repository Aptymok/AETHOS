import React, {useEffect, useState} from "react";
import { View, Text, Button, SafeAreaView } from "react-native";
import axios from "axios";
import io from "socket.io-client";

const API = "http://localhost:5000";

export default function App(){
  const [token, setToken] = useState(null);
  useEffect(()=>{
    // nothing fancy, in a real app use secure store
  },[]);

  const register = async () => {
    try {
      const r = await axios.post(`${API}/api/register`, {username:"mobile_user", password:"pass123"});
      setToken(r.data.token);
    } catch (e) {
      console.log(e.response?.data||e.message);
    }
  }

  const doDiag = async () => {
    try {
      const r = await axios.post(`${API}/api/diagnostic`, {query:"love change"}, {headers:{Authorization:`Bearer ${token}`}});
      console.log(r.data);
    } catch (e) {
      console.log(e.response?.data||e.message);
    }
  }

  return (
    <SafeAreaView style={{flex:1,alignItems:"center",justifyContent:"center", backgroundColor:"#111"}}>
      <Text style={{color:"#eee", fontSize:20, marginBottom:20}}>Levítico — laboratorio</Text>
      <Button title="Registrar demo" onPress={register} />
      <View style={{height:12}} />
      <Button title="Hacer diagnóstico" onPress={doDiag} disabled={!token}/>
    </SafeAreaView>
  )
}
