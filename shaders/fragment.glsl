#version 330 core

struct PointLight {
    vec3 position;
    vec3 color;
    float strenght;
};

in vec2 fragmentTexCoord;
in vec3 fragmentPos;
in vec3 fragmentNormal;

uniform sampler2D imageTexture;
//uniform PointLight Light;

out vec4 color;

vec3 calculatePointLight();

void main()
{
    vec3 temp = vec3(0.0);
    temp += calculatePointLight();
    color = vec4(temp, 1.0);
}

vec3 calculatePointLight(){
    vec3 result = vec3(0.0);
    vec3 baseTexture = texture(imageTexture, fragmentTexCoord).rgb;

    // ambient
    result += 0.2 * baseTexture;

    return result;
}