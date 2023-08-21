const checkuser = () => {
    const registrationform=document.form['registration']
    const emailformelement = registrationform['email']
    const email = emailformelement.value 
    const firstelement = registrationform('first')
    const first = firstelement.value 
    const secondelement = registrationform('second')
    const second = secondelement.value 
    const ageelement = registrationform('age')
    const age = ageelement.value 
    const genderelement = registrationform('gender')
    const gender = genderelement.value 
    const userelement = registrationform('user')
    const user = userelement.value 
    const passwdelement = registrationform('passwd')
    const passwd = passwdelement.value 
    axios.post('/validate',{
        email:email,
        age:age,
        gender:gender,
        user:user,
        passwd:passwd,
        first:first,
        second:second
    }
    )
    .then((response)=>{

    },(error)=>{

    }
    )
    
}
